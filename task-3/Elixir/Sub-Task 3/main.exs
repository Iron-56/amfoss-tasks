{n, _} = IO.gets("Enter rows: \n") |> Integer.parse

Enum.reduce(0..n-1, rem(n, 2), fn i, counter ->
    if counter == 0 do
        counter+2
    else
        stars = String.duplicate("*", counter)
        spaces = String.duplicate(" ", floor((n - counter) / 2))
        
        IO.puts(spaces <> stars <> spaces)
        
        if i < floor(n / 2), do: counter+2, else: counter-2
    end
end)
