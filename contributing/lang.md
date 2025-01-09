## Language Contributing

This is intended for anyone wishing to contribute translations to the project.

### License
All language files contained within amulet_map_editor/lang are licensed under the MIT license.
Any contributions you make to these files are made under the MIT license.
If you wish to contribute a new language it must include the MIT license header as found in the other files.
Upon creating a pull request you will be asked to confirm that you acknowledge this.

### Language Files
In order to support translations of text in the user interface all of the text has been moved into .lang files located in `amulet_map_editor/lang`.
The name of these lang files are RFC 1766 format language codes.
For example `en` for English, `en_US` for US English and `en_GB` for British English.
The lang files are formatted with one localised string per line with a `=` symbol separating the identifying key and the localised text.
The keys must only contain the characters a-z0-9_. and values can contain any character including the `=` symbol.

When loading the lang files, first the `en.lang` file is loaded to ensure that there is at least something for any given key.
If the language code contains an `_` symbol (for example `fr_CA`) then the lang file for the language section will be loaded next (`fr.lang`).
This allows languages that do not vary much between regions to share the same language file to minimise duplication.
Finally, if it exists, the region specific language file will be loaded which should only contain entries that vary between regions. 

### Branch Naming
A branch must be created in order to contribute to the project.
Unless you have permissions to create branches in Amulet-Team you will first need to [fork the repository](https://docs.github.com/en/github/getting-started-with-github/fork-a-repo).
You must then create a branch with an identifiable name using the following convention:

* When adding languages, use: `impl-lang-<langauge code>`
* When fixing languages, use: `improv-lang-<langauge code>`

### Pull Requests
Once you have added the desired changes you will need to [create a pull request](https://docs.github.com/en/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request). 
We ask that submitted Pull Requests give moderately detailed notes about the changes.

Once a Pull Request is submitted, we will mark the request for review.
Once that is done, we will review the changes and may provide feedback on things to change.
Once all additional changes have been made, we will merge the request.
