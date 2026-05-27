
errors = {}

Dir.glob('_terms/*.md').each do |file|
  lines = File.readlines(file)
  file_errors = []
  
  has_grammatical = false
  has_orthodox = false
  has_textual = false
  
  grammatical_term = nil
  
  in_front_matter = false
  yaml_content = ""
  
  lines.each_with_index do |line, i|
    if i == 0 && line.start_with?('---')
      in_front_matter = true
      next
    elsif in_front_matter && line.start_with?('---')
      in_front_matter = false
      next
    elsif in_front_matter
      yaml_content += line
      next
    end
    
    has_grammatical = true if line.include?('### Grammatical Analysis')
    has_orthodox = true if line.include?('### Orthodox Definition')
    has_textual = true if line.include?('### Textual References')
    
    # Try to extract the bold term under Grammatical Analysis
    if has_grammatical && !has_orthodox && line.match(/^\*\*(.*?)\*\*(:| \[)/)
      grammatical_term = $1
    end
  end
  
  require 'yaml'
  begin
    front_matter = YAML.safe_load(yaml_content)
    title = front_matter['title'] if front_matter
  rescue
    title = nil
  end
  
  file_errors << "Missing '### Grammatical Analysis'" unless has_grammatical
  file_errors << "Missing '### Orthodox Definition'" unless has_orthodox
  file_errors << "Missing '### Textual References'" unless has_textual
  
  if grammatical_term && title
    # compare them loosely (case-insensitive, ignoring macrons for basic match)
    t1 = grammatical_term.downcase.gsub(/[āīūṭḍṅñṇṃḷ]/, 'a' => 'ā', 'i' => 'ī', 'u' => 'ū', 't' => 'ṭ', 'd' => 'ḍ', 'n' => 'ñ', 'm' => 'ṃ', 'l' => 'ḷ') # this is just a rough transliteration check
    # Actually just check if they are totally different words
    if title.downcase.chars.first != grammatical_term.downcase.chars.first
      file_errors << "Title mismatch: Front matter says '#{title}', but body says '#{grammatical_term}'"
    end
  elsif has_grammatical
    file_errors << "Could not find bolded term under Grammatical Analysis."
  end
  
  errors[file] = file_errors unless file_errors.empty?
end

if errors.empty?
  puts "No structure/content mismatch errors found."
else
  errors.each do |file, errs|
    puts file
    errs.each { |e| puts "  - #{e}" }
  end
end
