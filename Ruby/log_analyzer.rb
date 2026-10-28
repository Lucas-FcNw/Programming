
#!/usr/bin/env ruby

abort "Usage: ruby log_analyzer.rb <log_file>" unless ARGV.length == 1

log_file = ARGV[0]
levels = %w[INFO WARN ERROR]
counts = Hash.new(0)

begin
  File.foreach(log_file) do |line|
    levels.each do |level|
      if line.match?(/\b#{level}\b/)
        counts[level] += 1
        break
      end
    end
  end

  puts "Log analysis: #{log_file}"
  puts "-" * 32

  levels.each do |level|
    puts format("%-8s %d", level, counts[level])
  end
rescue Errno::ENOENT
  abort "Error: file not found: #{log_file}"
rescue Errno::EACCES
  abort "Error: permission denied: #{log_file}"
end
