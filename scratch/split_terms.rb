
if ARGV.empty?
  puts "Usage: ruby scratch/split_terms.rb <bulk_file_path>"
  exit 1
end

bulk_file = ARGV[0]
unless File.exist?(bulk_file)
  puts "File not found: #{bulk_file}"
  exit 1
end

content = File.read(bulk_file)

# Regex to match the blocks
# Note: Use /m for multiline matching
blocks = content.scan(/---START_FILE: (.*?)---\n(.*?)\n---END_FILE: \1---/m)

blocks.each do |filename, body|
  target_path = File.join('_terms', filename)
  puts "Creating #{target_path}..."
  File.write(target_path, body)
end
puts "Done! Created #{blocks.size} files."
