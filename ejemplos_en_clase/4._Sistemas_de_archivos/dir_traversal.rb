#!/usr/bin/ruby
# coding: utf-8

@visitados = []

def muestra(dir)
  if @visitados.include?(dir)
    return
  end

  Dir.entries(dir).each do |d|
    next if d == '.' or d == '..'
    
    thisdir = File.join(dir, d)
    if File.directory?(thisdir) and File.readable?(thisdir)
      muestra(thisdir)
    end
    @visitados << thisdir
  end
end

muestra('/tmp')

puts @visitados.join("\n")
