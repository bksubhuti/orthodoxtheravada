require 'yaml'
require 'fileutils'
require 'optparse'

# Parse command line options
options = {
  mode: :dry,     # :dry or :write
  prefix: nil     # nil (all) or a string starting character/prefix
}

OptionParser.new do |opts|
  opts.banner = "Usage: ruby link_terms.rb [options]"

  opts.on("-w", "--write", "Actually write the links to the markdown files (modifies files)") do
    options[:mode] = :write
  end

  opts.on("-p", "--prefix PREFIX", "Only process terms whose filenames start with the given prefix (case-insensitive)") do |p|
    options[:prefix] = p.downcase
  end

  opts.on("-h", "--help", "Prints this help") do
    puts opts
    exit
  end
end.parse!

# 1. Collect all terms and their metadata
terms_dict = {}

Dir.glob('_terms/*.md').each do |file|
  slug = File.basename(file, '.md')
  content = File.read(file)
  
  if content =~ /\A---\n(.*?)\n---/m
    begin
      front_matter = YAML.safe_load($1)
      next unless front_matter
      
      terms_dict[slug] = {
        title: front_matter['title'],
        pali_spelling: front_matter['pali_spelling'],
        file: file
      }
    rescue => e
      puts "Error parsing YAML in #{file}: #{e.message}"
    end
  end
end

puts "Collected #{terms_dict.size} terms from _terms/ folder."

# 2. Function to build the regex matching pattern for a term slug
def build_pattern_for_term(slug, terms_dict)
  spellings = [slug]
  
  if terms_dict[slug]
    spellings << terms_dict[slug][:title] if terms_dict[slug][:title]
    spellings << terms_dict[slug][:pali_spelling] if terms_dict[slug][:pali_spelling]
  end
  
  # Remove nil, duplicates, and sort by length descending to match longer variants first
  spellings = spellings.compact.map(&:strip).reject(&:empty?).uniq.sort_by { |s| -s.length }
  
  # Escape spelling variants for regex
  escaped_spellings = spellings.map { |s| Regexp.escape(s) }
  
  # Define Pali word character set
  pali_chars = "a-zA-Z0-9āīūṭḍṅñṇṃḷĀĪŪṬḌṄÑṆṂḶ"
  
  # Return the pattern that matches any of these spellings with Unicode word boundaries
  "(?<![#{pali_chars}])(?:#{escaped_spellings.join('|')})(?![#{pali_chars}])"
end

# 3. Main process function
def process_linking(terms_dict, mode, prefix)
  puts "\n--- PROCESSING START (Mode: #{mode.to_s.upcase}, Prefix filter: #{prefix || 'NONE'}) ---"
  
  modified_files_count = 0
  total_replacements_count = 0
  
  terms_dict.each do |slug, info|
    next if prefix && !slug.start_with?(prefix)
    
    file = info[:file]
    content = File.read(file)
    
    # Separate front matter and body
    unless content =~ /\A(---\n.*?\n---)(.*)/m
      puts "Skipping #{file} (no front matter found)"
      next
    end
    
    front_matter_raw = $1
    body = $2
    
    begin
      front_matter = YAML.safe_load(front_matter_raw.sub(/\A---/, '').sub(/---\z/, ''))
      cross_links = front_matter['cross_links']
      
      next if !cross_links || cross_links.empty?
      
      # Build the combined skip pattern:
      # Group 1: code blocks, inline code, or already linked markdown
      skip_pattern = "(```.*?```|`[^`\n]+`|\\[[^\\]]+\\]\\([^)]+\\))"
      
      # We will scan the body and find matches for each cross_link
      file_replacements = 0
      updated_body = body.dup
      matches_summary = []
      
      cross_links.each do |link_slug|
        # Skip self-linking
        next if link_slug == slug
        
        # Build pattern for this specific target term
        term_pattern = build_pattern_for_term(link_slug, terms_dict)
        
        # Combined regex
        combined_regex = /#{skip_pattern}|(#{term_pattern})/mi
        
        # Perform replacement
        matches = []
        updated_body.gsub!(combined_regex) do |match|
          if $1
            # Matched a skip group (code, link), return untouched
            match
          else
            # Matched the target term! Let's wrap it in a link
            word = $2
            matches << word
            file_replacements += 1
            "[#{word}](/glossary/#{link_slug}/)"
          end
        end
        
        if matches.any?
          matches_summary << "'#{matches.uniq.join(', ')}' -> /glossary/#{link_slug}/"
        end
      end
      
      if file_replacements > 0
        total_replacements_count += file_replacements
        modified_files_count += 1
        
        action_word = (mode == :write) ? "Updated" : "Would update"
        puts "[#{action_word}] #{slug}.md:"
        matches_summary.each do |sum|
          puts "  - Linked #{sum}"
        end
        
        # If mode is :write, write the updated content back to the file
        if mode == :write
          new_content = front_matter_raw + updated_body
          File.write(file, new_content)
        end
      end
      
    rescue => e
      puts "Error processing #{file}: #{e.message}\n#{e.backtrace.join("\n")}"
    end
  end
  
  puts "\n--- PROCESSING COMPLETE ---"
  puts "Total files matching prefix/filter: #{terms_dict.keys.count { |k| prefix ? k.start_with?(prefix) : true }}"
  action_result = (mode == :write) ? "Modified" : "Would modify"
  puts "#{action_result} #{modified_files_count} files, adding #{total_replacements_count} links."
end

# Run the process
process_linking(terms_dict, options[:mode], options[:prefix])
