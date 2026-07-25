module Jekyll
  class PublishVerifiedOnly < Generator
    safe true
    priority :low

    def generate(site)
      # Only run if the setting is explicitly set to true
      return unless site.config['publish_only_verified']

      ['articles', 'terms', 'lists'].each do |col_name|
        collection = site.collections[col_name]
        next unless collection

        collection.docs.reject! do |doc|
          # A document is verified if its body content starts with "verified" (case insensitive)
          !doc.content.match?(/\A\s*verified/i)
        end
      end
    end
  end
end
