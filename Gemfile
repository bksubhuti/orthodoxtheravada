# Gemfile for Orthodox Theravada Website
# Works locally and on GitHub Pages with the Minimal Mistakes theme.

source "https://rubygems.org"

# Use GitHub Pages’ official Jekyll environment
gem "github-pages", group: :jekyll_plugins

# Plugins (used by both GitHub and local builds)
group :jekyll_plugins do
  gem "jekyll-feed", "~> 0.12"
  gem "jekyll-include-cache"
  gem "jekyll"
  gem "minimal-mistakes-jekyll"
  gem "jekyll-remote-theme"
end

# Windows and JRuby compatibility
platforms :mingw, :x64_mingw, :mswin, :jruby do
  gem "tzinfo", ">= 1", "< 3"
  gem "tzinfo-data"
end

# Required for Ruby 3.0+
gem "webrick", "~> 1.7"

# Performance booster for watching directories on Windows
gem "wdm", "~> 0.1", :platforms => [:mingw, :x64_mingw, :mswin]

# JRuby-specific parser fix
gem "http_parser.rb", "~> 0.6.0", :platforms => [:jruby]
