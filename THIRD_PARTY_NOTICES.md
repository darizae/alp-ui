# Third-party notices

`python-ui-library` source is MIT-licensed. The following dependencies and assets keep
their own licenses.

## Qt for Python / PySide6-Essentials

The package depends on `PySide6-Essentials` and uses only `QtCore`, `QtGui`, and
`QtWidgets`. Qt for Python community packages are offered under LGPLv3/GPLv3 terms;
this project selects the LGPLv3 path for eligible modules. `python-ui-library` does not
bundle Qt binaries in its wheel.

Applications that redistribute Qt are responsible for the applicable notices, license
text, corresponding-source route, and user replacement/relinking rights. See Qt's
[open-source obligations](https://www.qt.io/development/open-source-lgpl-obligations).

## Fonts

The wheel bundles unmodified static TrueType fonts under the SIL Open Font License 1.1.
The full upstream notices are shipped beside the files.

- DM Sans Regular, Medium, SemiBold, and Bold: copyright 2014 The DM Sans Project
  Authors; source revision `4412393b7d2de9fe7a92064c2dce9b5af5d7fd26` from
  [googlefonts/dm-fonts](https://github.com/googlefonts/dm-fonts).
- JetBrains Mono Regular, Medium, and SemiBold: copyright 2020 The JetBrains Mono
  Project Authors; source revision `19371302b95d218af43299bce79ddbddd0bc364d`
  from [JetBrains/JetBrainsMono](https://github.com/JetBrains/JetBrainsMono).

SHA-256 checksums:

```text
6a6924b35d757e32b21d611733d5b9a7bb6234b07b75334b0e2d2359985b26ee  DMSans-Bold.ttf
26af1a05d62906ffc3316ee6b4cbaf7ae86a1e607c5b9d89c64ec37f85063fbf  DMSans-Medium.ttf
a95a338942aa357145427be7c963ff691f9fe859c3512d9c0483e1914d57a208  DMSans-Regular.ttf
52897fabe96fa9dfe59b52681b57493f6bdce268ca3add5b82d701460ecc100d  DMSans-SemiBold.ttf
d16e6dc99672734698d629705f617c79f6eb6040f5113efe3a145204dc988109  JetBrainsMono-Medium.ttf
e6fd0d7e91550b3ed2b735d4312474362c4716edc4fc0577a0f61ed782d5aed1  JetBrainsMono-Regular.ttf
12d4b18fe6e1af528e4bea69cb0997aeff22f9e52fccffcf66342dd88aa32ab8  JetBrainsMono-SemiBold.ttf
```

## Design references

No source, icons, assets, or application text from the read-only Alpaca UI or
unlicensed TypeScript UI library references is redistributed by this project.
