#!/usr/bin/python3

"""Unit tests for metalfinder.scan"""

import os
import pickle

import pytest

import metalfinder.scan as mfs


@pytest.mark.parametrize("artist, filepath",
    [('Arch Enemy', 'tests/test_files/arch_enemy.flac'),
     ('Napalm Death', 'tests/test_files/napalm_death.flac')])
def test_get_artist_ok(artist, filepath):
    """Test get_artist() extracts the tag properly"""
    assert artist == mfs.get_artist(None, filepath)


def test_get_artist_no_tag():
    """Test get_artist() returns nothing when there is no artist tag"""
    assert mfs.get_artist(None, 'tests/test_files/no_artist.flac') is None


@pytest.mark.xfail(reason="Test not implemented yet.")
def test_get_artist_no_header():
    """Test get_artist() returns nothing when there is no FLAC header"""
    # This is hard to test, as we need to generate a flac file without a
    # header. TODO!
    assert False


def test_write_song_cache(tmpdir):
    """Test function write_song_cache()"""
    cachedir = tmpdir.join("cache")
    cachedir.mkdir()
    data = ['1', '2']
    mfs.write_song_cache(data, str(cachedir))
    song_cache_file = os.path.join(str(cachedir), 'song_cache')
    with open(song_cache_file, 'rb') as _cache:
        song_cache = pickle.load(_cache)
        assert song_cache == data


def test_get_song_cache(tmpdir):
    """Test function get_song_cache()"""
    cachedir = tmpdir.join("cache")
    cachedir.mkdir()
    data = ['1', '2']
    song_cache_file = os.path.join(str(cachedir), 'song_cache')
    with open(song_cache_file, 'wb') as _cache:
        pickle.dump(data, _cache)
    assert data == mfs.get_song_cache(str(cachedir))


def test_write_artist_cache(tmpdir):
    """Test function write_artist_cache()"""
    cachedir = tmpdir.join("cache")
    cachedir.mkdir()
    data = ['1', '2']
    mfs.write_artist_cache(data, str(cachedir))
    artist_cache_file = os.path.join(str(cachedir), 'artist_cache')
    with open(artist_cache_file, 'r', encoding='utf-8') as _cache:
        artist_cache = _cache.read()
        assert artist_cache == '1\n2'


def test_get_artist_cache(tmpdir):
    """Test function get_artist_cache()"""
    cachedir = tmpdir.join("cache")
    cachedir.mkdir()
    data = '1\n2'
    artist_cache_file = os.path.join(str(cachedir), 'artist_cache')
    with open(artist_cache_file, 'w', encoding='utf-8') as _cache:
        _cache.write(data)
    assert ['1', '2'] == mfs.get_artist_cache(str(cachedir))


@pytest.mark.xfail(reason="Test not implemented yet.")
def test_scan_dir():
    """Test function scan_dir()"""
    # This is a complex function and I'm tired :). TODO!
    assert False


@pytest.mark.xfail(reason="Test not implemented yet.")
def test_scan_wrapper():
    """Test wrapper function scan_wrapper()"""
    # TODO!
    assert False


def test_scan_broken_symlink(tmpdir):
    """test that we don't crash on broken symlinks (issues #21)"""
    cachedir = tmpdir.join("cache")
    cachedir.mkdir()
    musicdir = tmpdir.join("music")
    musicdir.mkdir()
    musicdir.join("brokensymlink.mp3").mksymlinkto("nonexistent")
    # we don't actually need the result here
    _ = mfs.scan_wrapper(musicdir, cachedir)
