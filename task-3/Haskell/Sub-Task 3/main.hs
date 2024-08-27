import Text.Printf

main :: IO ()
main = do
  putStr "Enter rows: "
  n <- readLn :: IO Int
  let counter = n `mod` 2
      buildRow i = do
        let stars = replicate counter '*'
            spaces = replicate (div (n - counter) 2) ' '
        printf "%s%s%s\n" spaces stars spaces
      nextCounter i counter = if i < div n 2 then counter + 2 else counter - 2
      buildPattern n counter =
        let updatedCounter = if counter == 0 then counter + 2 else counter
        in buildRow 0 updatedCounter : map (\i -> buildRow i (nextCounter i updatedCounter)) [1..n-1]

  mapM_ (flip buildRow) (buildPattern n counter)
