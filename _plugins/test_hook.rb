Jekyll::Hooks.register :site, :post_read do |site|
  puts "HOOK RUNNING! Terms size: #{site.collections['terms'].docs.size}"
end
