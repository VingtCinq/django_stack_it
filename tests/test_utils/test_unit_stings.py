from unittest import TestCase
from os import path
import sys
from stack_it.utils.strings import (
    camelcase,
    capitalcase,
    constcase,
    lowercase,
    pascalcase,
    pathcase,
    backslashcase,
    sentencecase,
    snakecase,
    spinalcase,
    dotcase,
    titlecase,
    trimcase,
    uppercase,
    alphanumcase,)


class StringcaseTest(TestCase):
    def test_camelcase(self):
        self.assertEqual('fooBar', camelcase('foo_bar'))
        self.assertEqual('fooBar', camelcase('FooBar'))
        self.assertEqual('fooBar', camelcase('foo-bar'))
        self.assertEqual('fooBar', camelcase('foo.bar'))
        self.assertEqual('barBaz', camelcase('_bar_baz'))
        self.assertEqual('barBaz', camelcase('.bar_baz'))
        self.assertEqual('', camelcase(''))
        self.assertEqual('none', camelcase(None))

    def test_capitalcase(self):

        self.assertEqual('', capitalcase(''))
        self.assertEqual('FooBar', capitalcase('fooBar'))

    def test_constcase(self):

        self.assertEqual('FOO_BAR', constcase('fooBar'))
        self.assertEqual('FOO_BAR', constcase('foo_bar'))
        self.assertEqual('FOO_BAR', constcase('foo-bar'))
        self.assertEqual('FOO_BAR', constcase('foo.bar'))
        self.assertEqual('_BAR_BAZ', constcase('_bar_baz'))
        self.assertEqual('_BAR_BAZ', constcase('.bar_baz'))
        self.assertEqual('', constcase(''))
        self.assertEqual('NONE', constcase(None))

    def test_lowercase(self):

        self.assertEqual('none', lowercase(None))
        self.assertEqual('', lowercase(''))
        self.assertEqual('foo', lowercase('Foo'))

    def test_pascalcase(self):

        self.assertEqual('FooBar', pascalcase('foo_bar'))
        self.assertEqual('FooBar', pascalcase('foo-bar'))
        self.assertEqual('FooBar', pascalcase('foo.bar'))
        self.assertEqual('BarBaz', pascalcase('_bar_baz'))
        self.assertEqual('BarBaz', pascalcase('.bar_baz'))
        self.assertEqual('', pascalcase(''))
        self.assertEqual('None', pascalcase(None))

    def test_pathcase(self):

        self.assertEqual('foo/bar', pathcase('fooBar'))
        self.assertEqual('foo/bar', pathcase('foo_bar'))
        self.assertEqual('foo/bar', pathcase('foo-bar'))
        self.assertEqual('foo/bar', pathcase('foo.bar'))
        self.assertEqual('/bar/baz', pathcase('_bar_baz'))
        self.assertEqual('/bar/baz', pathcase('.bar_baz'))
        self.assertEqual('', pathcase(''))
        self.assertEqual('none', pathcase(None))

    def test_sentencecase(self):

        self.assertEqual('Foo bar', sentencecase('foo_bar'))
        self.assertEqual('Foo bar', sentencecase('foo-bar'))
        self.assertEqual('Foo bar', sentencecase('foo.bar'))
        self.assertEqual('Bar baz', sentencecase('_bar_baz'))
        self.assertEqual('Bar baz', sentencecase('.bar_baz'))
        self.assertEqual('', sentencecase(''))
        self.assertEqual('None', sentencecase(None))

    def test_uppercase(self):

        self.assertEqual('NONE', uppercase(None))
        self.assertEqual('', uppercase(''))
        self.assertEqual('FOO', uppercase('foo'))

    def test_snakecase(self):

        self.assertEqual('foo_bar', snakecase('fooBar'))
        self.assertEqual('foo_bar', snakecase('foo_bar'))
        self.assertEqual('foo_bar', snakecase('foo-bar'))
        self.assertEqual('foo_bar', snakecase('foo.bar'))
        self.assertEqual('_bar_baz', snakecase('_bar_baz'))
        self.assertEqual('_bar_baz', snakecase('.bar_baz'))
        self.assertEqual('', snakecase(''))
        self.assertEqual('none', snakecase(None))

    def test_spinalcase(self):

        self.assertEqual('foo-bar', spinalcase('fooBar'))
        self.assertEqual('foo-bar', spinalcase('foo_bar'))
        self.assertEqual('foo-bar', spinalcase('foo-bar'))
        self.assertEqual('foo-bar', spinalcase('foo.bar'))
        self.assertEqual('-bar-baz', spinalcase('_bar_baz'))
        self.assertEqual('-bar-baz', spinalcase('.bar_baz'))
        self.assertEqual('', spinalcase(''))
        self.assertEqual('none', spinalcase(None))

    def test_titlecase(self):

        self.assertEqual('Foo Bar', titlecase('fooBar'))
        self.assertEqual('Foo Bar', titlecase('foo_bar'))
        self.assertEqual('Foo Bar', titlecase('foo-bar'))
        self.assertEqual('Foo Bar', titlecase('foo.bar'))
        self.assertEqual(' Bar Baz', titlecase('_bar_baz'))
        self.assertEqual(' Bar Baz', titlecase('.bar_baz'))
        self.assertEqual('', titlecase(''))
        self.assertEqual('None', titlecase(None))

    def test_trimcase(self):

        self.assertEqual('foo bar baz', trimcase(' foo bar baz '))
        self.assertEqual('', trimcase(''))

    def test_alphanumcase(self):

        self.assertEqual('FooBar', alphanumcase('_Foo., Bar'))
        self.assertEqual('Foo123Bar', alphanumcase('Foo_123 Bar!'))
        self.assertEqual('', alphanumcase(''))
        self.assertEqual('None', alphanumcase(None))
