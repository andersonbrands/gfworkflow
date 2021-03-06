# gfworkflow
A set of wrappers around git flow and [bump2version](https://github.com/c4urself/bump2version).

## Installation
You can use [pipx](https://pipxproject.github.io/pipx/) and have **gfworkflow** available via command line
```
pipx install gfworkflow
```
If you prefer you can also use pip:
```
pip install gfworkflow
```

> **Please note, bumping version is achieved through [bump2version](https://github.com/c4urself/bump2version), so make sure it is available via command line**

## Usage

#### Init git flow
Initializes git flow with default configuration, and adds **v** as version tag prefix
```
gfworkflow --init
```
... which is equivalent to:
```
git flow init -d -f
git config gitflow.prefix.versiontag v
```
#### Bump version
Bumps current version
```
gfworkflow --bump-version {part}
```
> **part** must be _major_, _minor_, _patch_ or custom part

... which is equivalent to:
```
bumpversion {part}
```

#### Start release
Starts a new release
```
gfworkflow --start-release {part}
```
> **part** must be _major_, _minor_, _patch_ or custom part

... which is equivalent to:
```
git flow release start {new_version}
```
... except that **new_version** is calculated with bump2version


#### Finish release
Finishes a release
```
gfworkflow --finish-release
```
... which is equivalent to:
```
git flow release finish -m " - " {release_version}
```
... except that it gets **release_version** from current branch

#### Bump release
Bumps a release, which means to:
1. Start release
2. Bump version
3. Finish release

```
python workflow --bump-release {part}
```
> **part** must be _major_, _minor_, _patch_ or custom part


### v0.1.0