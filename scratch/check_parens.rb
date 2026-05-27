
errors = []

Dir.glob('_terms/*.md').each do |file|
  lines = File.readlines(file)
  lines.each_with_index do |line, i|
    clean_line = line.gsub(/\[.*?\]/, '') # remove brackets
    open_p = clean_line.count('(')
    close_p = clean_line.count(')')
    if open_p != close_p
      errors << "#{file}:#{i+1}: Unbalanced parentheses: #{line.strip}"
    end
  end
end

if errors.empty?
  puts "No unbalanced parentheses."
else
  puts errors
end
