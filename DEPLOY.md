
Deployment of dtumathtools
==========================

The deployment of `dtumathtools` will go a bit beyond regular SemVer methods.

The minimal release cycle of `dtumathtools` will be twice a year.

The versions will be named:

- YYYY.SEMESTER.FIX
  where YYYY is the year, and SEMESTER will be one of:

  * 1 for the spring semester
  * 2 for the autumn semester

  This will clarify to students what we relase etc.
  Sadly, pypi does not allow letters in the version numbers
  released. Hence this number convention.

  It has been determined that additional semesters are not needed
  since it would be a superfluous burden for the maintainers.

  FIX will be a consecutive numbering, starting from 0, that fixes problems
  for the release. Generally we don't think these will be used, since
  testing them is implicit. However, in rare cases it might be useful to
  maintain a set of fixes.


Every YYYY.SEMESTER will be supported for ~6 years (due to student requirement).
And hence, we must employ a branch structure for each of them.

Once released the releases will be released on PyPi and conda-forge.

The procedure will be something like this:

1. Create a new branch for the release (if not already done), the
   name will be "bYYYY.SEMESTER".
2. Create an annotated tag for the release "vYYYY.SEMESTER.FIX".
3. Check that PyPi works.
4. Create conda-forge releases. Again, to support multiple releases,
   we must employ a branch-structure there. They will be supported for
   6 years, then branch-deletion will occur.
