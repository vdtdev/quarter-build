Quarter-Life Build System
=================


### Contents ###
>
1. [Overview](#overview)
- [Files](#files)
- [Required Modules](#modules)
2. [QLBuild](#qlbuild)
- [Usage](#qlbusage)
- [Classes](#qlbclasses)
3. [QLQC](#qlqc)

<a name="overview"></a>

##Overview##

Quarter-Life Build is a Python based build system for Source engine mods. It automates the process of building models, materials, and managing multiple revisions of script and resource files.

###Files###
<a name="files"/>
>
-   `qbe.py` v0.20 of main qlb module (Left for reference, obsolete)
-   `qlbs.ini` Contains definitions of the required path variables
-  `qlbuild.py`- v0.2x of main qlb module, contains multiple classes (current)
-   `qlqc.py` - QL QC Model compiler tool
-   `cltest.py` - Initial implementation of QLQC (left for reference, obsolete)

###Python Modules Required###
>
+ `textwrap`
+ `os`
+ `string`
+ `time`
+ `argparse`
+ `sys`

<a name="qlbuild"></a>

QLBuild
-------

<a name="qlbusage"/>

###Usage###
>    
    qlbuild.py [-h] [--args {U,C,N,A}] action target

__Arguments__

Argument | Optional | Values | Help
:--------|:--------:|:-------|:--------------------
action | _no_ | get, set, build | Specifies the type of action to perform
target | _no_ | assets, materials | Specifies the content type that the action is to be performed on
--args [a] | _yes_ |_see [args](qlbargs)_ | Target-specific options

<a name="qlbargs"/>

__Target Specific Arguments__

Argument | Targets | Actions | Help
:----:|:--------|:--------|:-----
U | materials, assets | get, put | Copy updated files only
C | materials, assets | get, put | Copy modified files only
N | materials, assets | get, put | Copy new files only
A | materials, assets | get, put | Copy all files (default)

<a name="qlbclasses"/>

###Classes###
- __asset_management__
> Handles all actions performed targetting `assets` 
- __config__
> Loads qlb .ini file and provides access to the variables defined within it


