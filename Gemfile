# frozen_string_literal: true

source "https://rubygems.org"

# ✅ Jekyll 본체
gem "jekyll", "~> 4.4.1"

# Chirpy 테마 Gem 사용 (GitHub에서 가져옴)
gem "jekyll-theme-chirpy", "~> 7.0", ">= 7.0.1"

# ✅ 테스트 도구
group :test do
  gem "html-proofer", "~> 5.0"
end

# ✅ Windows 플랫폼 관련
platforms :mingw, :x64_mingw, :mswin, :jruby do
  gem "tzinfo", ">= 1", "< 3"
  gem "tzinfo-data"
end

gem "wdm", "~> 0.2.0", platforms: [:mingw, :x64_mingw, :mswin]

# ✅ Jekyll 플러그인
group :jekyll_plugins do
  gem "jekyll-sitemap"
  gem "jekyll-google-tag-manager"
end

# ✅ 로깅 도구
gem "logger"
