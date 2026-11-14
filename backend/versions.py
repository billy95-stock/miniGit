"""Création, listing et restauration des versions (snapshots)"""

from datetime import datetime

def compare(old, new) :
	added = set(new) - set(old)
	deleted = set(old) - set(new)
	common = set(old) & set(new)
	modified = []
	for path in common :
		if old[path] != new[path]:
			modified.append(path)
	return {
		"added" : sorted(added),
		"modified" : sorted(modified),
		"deleted" : sorted(deleted),
	}

def create_version(history, state, manual=False) :
	if history :
		last_state = history[-1]["files"]
	else :
		last_state = {}
	changes = compare(last_state, state)
	if not changes["added"] and not changes["modified"] and not changes["deleted"] :
		return None
	number = len(history) + 1
	date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	version = {
		"number": number,
		"date": date,
		"type": "manuel" if manual else "auto",
		"files": state,
		"changes": changes,
	}
	history.append(version)
	return version