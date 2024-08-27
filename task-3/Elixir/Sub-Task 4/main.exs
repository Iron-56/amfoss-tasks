
File.write("output.txt","")

defmodule FS do
    def read_first_line() do
      case File.read("input.txt") do
        {:ok, content} -> content
          
        {:error, reason} ->
          IO.puts("Failed to read file: #{reason}")
          nil
      end
    end
end

{n, _} = FS.read_first_line() |> Integer.parse

Enum.reduce(0..n-1, rem(n, 2), fn i, counter ->
    if counter == 0 do
        counter+2
    else
        stars = String.duplicate("*", counter)
        spaces = String.duplicate(" ", floor((n - counter) / 2))
        
        line = spaces <> stars <> spaces <> "\n"
        File.write("output.txt", line, [:append])
        
        if i < floor(n / 2), do: counter+2, else: counter-2
    end
end)