#!/usr/bin/env ruby
# link_terms.rb — Cross-link ALL Pāḷi glossary terms across _terms/
#
# Unlike the original script which only linked terms from cross_links,
# this scans every term page's body for ANY mention of ANY other glossary
# term and links the first occurrence of each.
#
# Safety guarantees:
#   - Never double-links (preserves all existing [text](/glossary/slug/) links)
#   - Never self-links (a page won't link to its own term)
#   - Only links FIRST occurrence of each target term per file
#   - Handles *italic*, **bold**, and ***bold-italic*** wrapped terms
#   - Skips text inside the bold term definition on the Grammatical Analysis line
#   - Case-insensitive matching with full Pāḷi diacritics support
#
# Usage:
#   ruby scratch/link_terms.rb                  # dry run, all files
#   ruby scratch/link_terms.rb -p a             # dry run, files starting with 'a'
#   ruby scratch/link_terms.rb -w               # WRITE mode, all files
#   ruby scratch/link_terms.rb -w -p jh         # WRITE mode, files starting with 'jh'
#   ruby scratch/link_terms.rb -v               # verbose dry run

require 'yaml'
require 'set'
require 'optparse'

options = { mode: :dry, prefix: nil, verbose: false }
OptionParser.new do |opts|
  opts.banner = "Usage: ruby scratch/link_terms.rb [options]"
  opts.on("-w", "--write",          "Write changes (default: dry run)")          { options[:mode] = :write }
  opts.on("-p", "--prefix PREFIX",  "Only process files starting with PREFIX")   { |p| options[:prefix] = p.downcase }
  opts.on("-v", "--verbose",        "Show each individual link added")           { options[:verbose] = true }
  opts.on("-h", "--help",           "Show help") { puts opts; exit }
end.parse!

# ═══════════════════════════════════════════════════════════════════════════════
# Step 1: Load all terms
# ═══════════════════════════════════════════════════════════════════════════════

terms = {}  # slug → { title:, pali:, file: }

Dir.glob('_terms/*.md').sort.each do |file|
  slug = File.basename(file, '.md')
  raw = File.read(file)
  next unless raw =~ /\A---\n(.*?)\n---/m
  fm = YAML.safe_load($1) rescue next
  next unless fm
  terms[slug] = {
    title: fm['title']&.strip,
    pali:  fm['pali_spelling']&.strip,
    file:  file
  }
end

puts "Loaded #{terms.size} terms."

# ═══════════════════════════════════════════════════════════════════════════════
# Step 2: Build spelling → slug lookup (longest spelling wins ties)
# ═══════════════════════════════════════════════════════════════════════════════

# spelling_to_slug: downcased surface form → slug
spelling_to_slug = {}
# original_case: downcased → original case (for display)
original_case = {}

terms.each do |slug, info|
  [info[:title], info[:pali], slug].compact.reject(&:empty?).each do |form|
    key = form.downcase
    # Prefer the entry whose slug matches the form, or else the longer slug
    if spelling_to_slug[key].nil?
      spelling_to_slug[key] = slug
      original_case[key] = form
    end
  end
end

# Build sorted list of all surface forms, longest first
all_forms = spelling_to_slug.keys.sort_by { |k| -k.length }

# Pāḷi word-boundary chars
PC = 'a-zA-Z0-9āīūṭḍṅñṇṃḷĀĪŪṬḌṄÑṆṂḶ\-'

# Build the master regex
escaped_forms = all_forms.map { |f| Regexp.escape(original_case[f]) }
TERM_PATTERN = Regexp.new(
  "(?<![#{PC}])(#{escaped_forms.join('|')})(?![#{PC}])",
  Regexp::IGNORECASE
)

# ═══════════════════════════════════════════════════════════════════════════════
# Step 3: Process files
# ═══════════════════════════════════════════════════════════════════════════════

total_files_modified = 0
total_links_added = 0

terms.each do |slug, info|
  next if options[:prefix] && !slug.start_with?(options[:prefix])

  content = File.read(info[:file])
  unless content =~ /\A(---\n.*?\n---)(.*)/m
    puts "SKIP #{slug}.md — no front matter" if options[:verbose]
    next
  end

  fm_raw = $1
  body   = $2

  # ── Collect slugs already linked in this file ──
  already_linked = Set.new
  body.scan(/\[[^\]]*\]\(\/glossary\/([^\/]+)\/\)/) { |m| already_linked << m[0] }

  # ── Split body into "protected" (existing links) and "free" segments ──
  # We process only the free segments for new linking.
  #
  # Protected patterns: [text](url) — existing markdown links
  # We also protect the **BoldTerm**: line in Grammatical Analysis

  segments = []
  pos = 0
  # Match existing markdown links
  body.scan(/\[[^\]]*\]\([^)]*\)/) do |match|
    match_start = $~.begin(0)
    match_end   = $~.end(0)
    if match_start > pos
      segments << { type: :free, text: body[pos...match_start] }
    end
    segments << { type: :protected, text: match }
    pos = match_end
  end
  segments << { type: :free, text: body[pos..] } if pos < body.length

  # ── Now linkify each free segment ──
  linked_in_file = already_linked.dup
  file_links_added = []

  new_segments = segments.map do |seg|
    next seg if seg[:type] == :protected

    text = seg[:text]
    result = ""
    scan_pos = 0

    while scan_pos < text.length
      m = TERM_PATTERN.match(text, scan_pos)
      break unless m

      matched_word = m[1]
      ms = m.begin(0)
      me = m.end(0)

      target_slug = spelling_to_slug[matched_word.downcase]

      # ── Should we skip this match? ──
      skip = false
      skip = true if target_slug.nil?
      skip = true if target_slug == slug                    # self-link
      skip = true if linked_in_file.include?(target_slug)  # already linked

      # Skip if inside a **bold definition** line (Grammatical Analysis heading)
      unless skip
        line_start = text.rindex("\n", [ms - 1, 0].max) || 0
        line_text = text[line_start...(text.index("\n", me) || text.length)]
        skip = true if line_text.include?("### Grammatical Analysis")
        # Skip the bold term definition line: **Term**: [...]
        skip = true if line_text.match?(/\A\s*\*\*[^*]+\*\*\s*:?\s*\[/)
      end

      if skip
        result << text[scan_pos...me]
        scan_pos = me
        next
      end

      # ── Append text before the match ──
      result << text[scan_pos...ms]

      # ── Handle wrapping in *italics* or **bold** ──
      before = result
      after  = text[me..]

      if before.end_with?('*') && !before.end_with?('**') &&
         after&.start_with?('*') && !after&.start_with?('**')
        # *term* → *[term](/glossary/slug/)*
        result = result[0..-2]  # strip trailing *
        result << "*[#{matched_word}](/glossary/#{target_slug}/)*"
        scan_pos = me + 1       # skip closing *
      elsif before.end_with?('**') && after&.start_with?('**')
        # **term** → **[term](/glossary/slug/)**
        result = result[0..-3]
        result << "**[#{matched_word}](/glossary/#{target_slug}/)**"
        scan_pos = me + 2
      elsif before.end_with?('***') && after&.start_with?('***')
        # ***term*** → ***[term](/glossary/slug/)***
        result = result[0..-4]
        result << "***[#{matched_word}](/glossary/#{target_slug})***"
        scan_pos = me + 3
      else
        result << "[#{matched_word}](/glossary/#{target_slug}/)"
        scan_pos = me
      end

      linked_in_file << target_slug
      file_links_added << "#{matched_word} → /glossary/#{target_slug}/"
    end

    result << text[scan_pos..] if scan_pos < text.length
    { type: :free, text: result }
  end

  new_body = new_segments.map { |s| s[:text] }.join

  if file_links_added.any?
    total_files_modified += 1
    total_links_added += file_links_added.size

    label = (options[:mode] == :write) ? "UPDATED" : "would update"
    puts "[#{label}] #{slug}.md (+#{file_links_added.size} links)"

    if options[:verbose]
      file_links_added.each { |l| puts "    #{l}" }
    end

    if options[:mode] == :write
      File.write(info[:file], fm_raw + new_body)
    end
  end
end

puts "\n#{'═' * 50}"
puts "Mode: #{options[:mode].upcase}"
puts "Files modified: #{total_files_modified}"
puts "Links added: #{total_links_added}"
puts "#{'═' * 50}"
