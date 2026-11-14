"""Création, listing et restauration des versions (snapshots)"""

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