"""Création, listing et restauration des versions (snapshots)"""

from datetime import datetime
import time
from pathlib import Path

#fonction qui compare la dernier version dans history et celle de actuelle de notre PC
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

#fonction qui ajoute un version dans history
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

#fonction qui liste dans result un history
def list_versions(history) :
	result = []
	for version in history :
		result.append({
			"number": version["number"],
			"date": version["date"],
			"type": version["type"],
			"changes": version["changes"],
		})
	return result

#fonction qui regarde toute les check_interval
#qui fait creer une sauvegarde dans history quand on a fait plus aucune
#modification au bout de stabilization_delay
def watch_loop(history, config, scan) :
	folder = config["watched_folders"][0]
	interval = config["check_interval"]
	delay = config["stabilization_delay"]
	last_seen = scan(folder)
	last_change = time.time()
	while True :
		time.sleep(interval)
		state = scan(folder)
		if state != last_seen :
			last_seen = state
			last_change = time.time()
		elif time.time() - last_change >= delay :
			create_version(history, state)

#fonction pour sauvgarder manuellement
def save_now(history, config, scan) :
	folder = config["watched_folders"][0]
	state = scan(folder)
	return create_version(history, state, manual=True)


def restore(history, number, target, read_file) :
	files = None
	for version in history :
		if version["number"] == number :
			files = version["files"]
	if files is None :
		raise ValueError(f"Version {number} introuvable")
	for path, sha in files.items() :
		dest = Path(target) / path
		if sha is None :
			dest.mkdir(parents=True, exist_ok=True)
		else :
			dest.parent.mkdir(parents=True, exist_ok=True)
			dest.write_bytes(read_file(sha))