from distutils.core import setup

setup(
    name="signalgen",
    version="0.2",
    description="Generate a waveform at audio ranges (0-20,000Hz).",
    author="Matthew Brush",
    author_email="mbrush AT leftclick DOT ca",
    url="https://github.com/codebrainz/signalgen",
    license="GPLv3",
    packages=["signalgen"],
    provides=["signalgen"],
    requires=["gst", "urwid"],
    scripts=["runner/signalgen"]
)

