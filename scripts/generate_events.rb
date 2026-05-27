require 'open-uri'
require 'json'
require 'date'
require 'time'

ICS_URL = "https://calendar.google.com/calendar/ical/a9990f54cc62171dfef7a892c552c8964dc1a18735784e6d8c36803ce3cffb9b%40group.calendar.google.com/public/basic.ics"

ics = URI.open(ICS_URL).read

events = []

ics.split("BEGIN:VEVENT")[1..]&.each do |block|
  body = block.split("END:VEVENT")[0]

  summary = body[/SUMMARY:(.+)/,1]&.strip
  next unless summary

  # DTSTART handling
  start_raw =
    if body =~ /DTSTART;VALUE=DATE:(\d{8})/
      d = Date.strptime($1, "%Y%m%d")
      Time.utc(d.year, d.month, d.day, 12, 0, 0) # normalize to noon UTC
    else
      raw = body[/DTSTART(?:;[^:]+)?:([0-9T]+Z?)/,1]
      begin
        Time.parse(raw).utc
      rescue
        nil
      end
    end

  next unless start_raw

  events << {
    summary: summary,
    startRaw: start_raw.iso8601,
    allDay: (body =~ /DTSTART;VALUE=DATE:/ ? true : false)
  }
end

# sort by actual date only (ignore google push delay)
events.sort_by! { |e| Time.parse(e[:startRaw]) }

File.write("assets/events.json", JSON.pretty_generate({
  generatedAt: Time.now.utc.iso8601,
  events: events
}))

puts "Generated assets/events.json with #{events.size} events"
puts File.read("assets/events.json")  # SHOW EXACT JSON IN WORKFLOW LOG
