import struct
import sys

def recover_flag(img_path):
    with open(img_path, "rb") as f:
        # Seek to custom filesystem start
        f.seek(0x1000)
        header = f.read(16)
        
        if len(header) < 16:
            print("[-] Error: Image too small.")
            return

        # Unpack Superblock: Magic (4s), BlockSize (H), TotalBlocks (I), FlagInode (I)
        magic, block_size, total_blocks, flag_inode = struct.unpack('<4s H I I 2x', header)
        
        if magic != b'TBFS':
            print(f"[-] Error: Invalid Magic {magic}. Are you at 0x1000?")
            return

        print(f"[+] Found Custom Filesystem!")
        print(f"    Block Size: {block_size}")
        print(f"    Total Blocks: {total_blocks}")
        print(f"    Flag Inode: 0x{flag_inode:X}")
        
        print("\n[+] Attempting Flag Recovery...")
        recovered_data = b""
        
        for i in range(total_blocks):
            # Calculate block offset
            offset = flag_inode + (i * block_size)
            f.seek(offset)
            
            # Read first 4 bytes of the block (the flag chunk)
            chunk = f.read(4)
            
            # TODO: We observed some high entropy in the data. 
            # Could there be an additional encoding layer?
            # For now, just appending raw bytes.
            recovered_data += chunk
            
        print(f"\n[!] Recovered Data: {recovered_data}")
        print("[!] Warning: Data appears corrupted. Check spatial consistency.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 parser.py <challenge.img>")
    else:
        recover_flag(sys.argv[1])
