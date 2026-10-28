
use sha2::{Digest, Sha256};
use std::{
    env,
    fs::File,
    io::{self, Read},
    process,
};

fn calculate_sha256(path: &str) -> io::Result<String> {
    let mut file = File::open(path)?;
    let mut hasher = Sha256::new();
    let mut buffer = [0u8; 8192];

    loop {
        let bytes_read = file.read(&mut buffer)?;

        if bytes_read == 0 {
            break;
        }

        hasher.update(&buffer[..bytes_read]);
    }

    Ok(format!("{:x}", hasher.finalize()))
}

fn main() {
    let path = env::args().nth(1).unwrap_or_else(|| {
        eprintln!("Usage: file_integrity <file_path>");
        process::exit(1);
    });

    match calculate_sha256(&path) {
        Ok(hash) => {
            println!("File: {path}");
            println!("SHA-256: {hash}");
        }
        Err(error) => {
            eprintln!("Failed to read file: {error}");
            process::exit(1);
        }
    }
}
