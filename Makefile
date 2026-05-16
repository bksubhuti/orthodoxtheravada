serve:
	JEKYLL_NO_BUNDLER_REQUIRE=1 bundle exec jekyll serve --config _config.yml,_config_local.yml --livereload --future

build:
	bundle exec jekyll build

.PHONY: serve build
