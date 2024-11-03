
General Info:


(-) Converts an Apple Music playlist to Spotify.


(-) One needs to assign his own Spotify Client ID, API Secret, User ID & USERNAME inside of am2sp.py.


(-) Python IDE app is required in iPhone (PYTO is used inside the am2sp.shortcut).


(-) One needs to import am2sp.shortcut which its original goal was to first extract an Apple Music playlist, and then pass its tracks to am2sp.py. Due to iOS limitations, a temporary workaround was created, in which a JSON file is created out of the Apple Music playlist's content, which is sent to a given email as well as saved locally => then it is passed to a similar am2sp.py script on PC.


(-) not_found.txt => contains Apple Music items not found during Spotify conversion process. It is filled with "Error Log".shortcut