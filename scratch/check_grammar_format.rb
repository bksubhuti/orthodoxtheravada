
errors = []

Dir.glob('_terms/*.md').each do |file|
  lines = File.readlines(file)
  
  grammatical_line = lines.find { |l| l.start_with?('**') && l.include?('**:') }
  
  if grammatical_line
    unless grammatical_line.include?('[') && grammatical_line.include?(']')
      errors << "#{file}: Grammatical line missing gender bracket [ ]: #{grammatical_line.strip}"
    end
  end
end

if errors.empty?
  puts "No gender bracket formatting errors."
else
  puts errors
end
