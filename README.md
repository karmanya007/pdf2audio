# PDF2MP3

A simple commandline app for searching and looking up opensource vulnerabilities
For windows only(Requires pywin32 package)

# Installation

## Using Pip

```bash
  $ pip install pdf2mp3
```
## Manual

```bash
  $ git clone https://github.com/karmanya007/pdf2audio
  $ cd pdf2mp3
  $ python setup.py install
```
# Usage

```bash
$ pdf2mp3
```
## Convert
`convert <pathToPdf> [options]`
<br>

`Options:`
<br>

`-n (--name) : Name of the mp3 file (Default : test)`
```bash
$ pdf2mp3 convert C:\Users\example.pdf
OR
$ pdf2mp3 convert C:\Users\example1.pdf -n my_mp3_file
```
