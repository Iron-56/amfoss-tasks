
use std::io;

fn main() {
    println!("Enter rows: ");
    
	let mut input_line = String::new();
	io::stdin()
		.read_line(&mut input_line)
		.expect("Failed to read line");
	let n: i32 = input_line.trim().parse().expect("Input not an integer");

	let mut counter: i32 = n%2;

	for i in 0..n {
		if counter == 0 {
			counter += 2;
	 		continue;
		}
		let fv: f32 = ((n-counter) as f32)/2.0;
        let c1 = counter as usize;
        let c2 = (fv.floor() as i32) as usize;

		let stars = "*".repeat(c1);
		let spaces = " ".repeat(c2);

		if i < ((n as f32)/2.0).floor() as i32 {
 			counter += 2;
		} else {
			counter -= 2;
		}

		print!("{}\n", spaces + &stars);
	}
}