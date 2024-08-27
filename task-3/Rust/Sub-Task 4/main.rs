
use std::fs;
use std::fs::OpenOptions;
use std::io::Write;

fn main() {
    
    let mut file = OpenOptions::new()
        .write(true)
        .append(true)
        .open("output.txt")
        .unwrap();
    
    let mut input_line = fs::read_to_string("input.txt").unwrap();

    let n = match input_line.trim().parse::<i32>() {
        Ok(num) => num,
        Err(_) => {
            println!("Invalid input. Please enter an integer.");
            return;
        }
    };

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
        
        let formatted_line = format!("{}{}", spaces, stars);
        if let Err(e) = write!(file, "{}\n", formatted_line) {
            println!("Couldn't write to file: {}", e);
        }
	}
}