#!/bin/bash
export PATH="/opt/homebrew/opt/ruby@3.1/bin:$PATH"
cd /Users/lyan/Documents/orthodoxtheravada
JEKYLL_NO_BUNDLER_REQUIRE=1 bundle exec jekyll serve --config _config.yml,_config_local.yml --livereload --future
