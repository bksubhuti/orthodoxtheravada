
require 'yaml'

errors = []

Dir.glob('_terms/*.md').each do |file|
  lines = File.readlines(file)
  yaml_content = ""
  in_front_matter = false
  grammatical_term = nil
  has_grammatical = false
  
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
    
    if has_grammatical && line.match(/^\*\*(.*?)\*\*(:| \[)/)
      grammatical_term = $1
      break
    end
  end
  
  begin
    front_matter = YAML.safe_load(yaml_content)
    title = front_matter['title']
    pali_spelling = front_matter['pali_spelling']
    
    if title && grammatical_term
      # Strip macrons for comparison or compare exact
      # Let's check exact match, ignoring case
      t_norm = title.downcase.strip
      g_norm = grammatical_term.downcase.strip
      p_norm = pali_spelling ? pali_spelling.downcase.strip : ""
      
      if t_norm != g_norm
        errors << "#{file}: Title '#{title}' != Grammatical Term '#{grammatical_term}'"
      end
      
      if p_norm != g_norm && p_norm != ""
        errors << "#{file}: Pali Spelling '#{pali_spelling}' != Grammatical Term '#{grammatical_term}'"
      end
    end
  rescue
  end
end

if errors.empty?
  puts "No spelling mismatches found."
else
  puts errors
end
