
require 'yaml'

Dir.glob('_terms/*.md').each do |file|
  content = File.read(file)
  if content =~ /\A---\n(.*?)\n---/m
    front_matter = YAML.safe_load($1)
    
    # Check if arrays are actually arrays
    ['cross_links', 'canonical_texts', 'commentaries'].each do |field|
      val = front_matter[field]
      if val && !val.is_a?(Array)
        puts "#{file}: #{field} is not an array: #{val.inspect}"
      end
    end
    
    # check for weird quotes or typos
    if front_matter['pali_spelling'] && front_matter['pali_spelling'].include?('"')
      puts "#{file}: pali_spelling has weird quotes: #{front_matter['pali_spelling']}"
    end
  end
end
puts "Front matter check complete."
