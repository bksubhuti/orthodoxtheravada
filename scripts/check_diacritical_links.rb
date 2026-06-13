#!/usr/bin/env ruby
# frozen_string_literal: true

# check_diacritical_links.rb
# Scans _terms/*.md and _lists/*.md for /glossary/ links containing
# diacritical characters (ā, ī, ū, ṭ, ḍ, ṅ, ñ, ṇ, ḷ, ṃ, etc.)
# which will produce broken URL-encoded paths on the site.
#
# Usage:
#   ruby scripts/check_diacritical_links.rb          # report only
#   ruby scripts/check_diacritical_links.rb --fix     # auto-fix in place

require 'fileutils'

DIACRITICAL_MAP = {
  'ā' => 'a', 'ī' => 'i', 'ū' => 'u',
  'ṭ' => 't', 'ḍ' => 'd', 'ṅ' => 'n',
  'ñ' => 'n', 'ṇ' => 'n', 'ḷ' => 'l',
  'ṃ' => 'm', 'ṁ' => 'm', 'ś' => 's',
  'ṣ' => 's', 'ḥ' => 'h',
  'Ā' => 'a', 'Ī' => 'i', 'Ū' => 'u',
  'Ṭ' => 't', 'Ḍ' => 'd', 'Ṅ' => 'n',
  'Ñ' => 'n', 'Ṇ' => 'n', 'Ḷ' => 'l',
  'Ṃ' => 'm', 'Ś' => 's', 'Ṣ' => 's',
  'Ḥ' => 'h'
}.freeze

DIACRITICAL_REGEX = /[āīūṭḍṅñṇḷṃṁśṣḥĀĪŪṬḌṄÑṆḶṂŚṢḤ]/

# Match markdown links whose URL path contains diacriticals
# e.g. [Aṭṭhakathā](/glossary/aṭṭhakathā/)
LINK_REGEX = %r{\[([^\]]*)\]\((/glossary/[^)]*#{DIACRITICAL_REGEX}[^)]*)\)}

def strip_diacriticals(slug)
  slug.gsub(DIACRITICAL_REGEX) { |ch| DIACRITICAL_MAP[ch] || ch }
end

def scan_file(path, fix: false)
  content = File.read(path, encoding: 'utf-8')
  findings = []

  content.scan(LINK_REGEX) do |display_text, url|
    fixed_url = strip_diacriticals(url)
    findings << {
      file: path,
      display: display_text,
      bad_url: url,
      fixed_url: fixed_url
    }
  end

  if fix && !findings.empty?
    new_content = content.gsub(LINK_REGEX) do |_match|
      display = Regexp.last_match(1)
      url     = Regexp.last_match(2)
      fixed   = strip_diacriticals(url)
      "[#{display}](#{fixed})"
    end
    File.write(path, new_content)
  end

  findings
end

# --- Main ---
fix_mode = ARGV.include?('--fix')
dirs = %w[_terms _lists]
root = File.expand_path('..', __dir__)

all_findings = []

dirs.each do |dir|
  full_dir = File.join(root, dir)
  next unless Dir.exist?(full_dir)

  Dir.glob(File.join(full_dir, '*.md')).sort.each do |path|
    all_findings.concat(scan_file(path, fix: fix_mode))
  end
end

if all_findings.empty?
  puts "✅ No diacritical glossary links found. All links are clean."
else
  puts "#{fix_mode ? '🔧 FIXED' : '⚠️  FOUND'} #{all_findings.size} diacritical link(s):\n\n"
  all_findings.each do |f|
    rel = f[:file].sub("#{root}/", '')
    puts "  #{rel}"
    puts "    #{f[:bad_url]}"
    puts "    → #{f[:fixed_url]}"
    puts
  end

  unless fix_mode
    puts "Run with --fix to auto-correct these links:"
    puts "  ruby scripts/check_diacritical_links.rb --fix"
  end
end
