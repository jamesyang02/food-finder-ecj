'use client'

import Image from 'next/image';
import { useState } from 'react';
import axios from 'axios';

export default function FileUpload() {
  const [file, setFile] = useState<File>();

  const handleSubmission = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    if (!file) return;
    const base64 = await toBase64(file as File);

    // Call the FoodVisor query
    const formData = new FormData();
    formData.append('file', file);
    axios.post('https://food-finder-dr3kfl0iz-james-yangs-projects-b85f648d.vercel.app/api/analyze', formData)
    .then((res) => {    
      console.log(res.data);
    })
    .catch((err) => {
      console.error(err);
      console.log("Something went wrong while uploading your image.");
    });
    // const chatCompletion = await main(base64 as string);
    // console.log(chatCompletion.choices[0]?.message?.content || "");
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      // Check if file is too big, max size is 5MB
      if (file.size > 1024 * 1024 * 5) {
        alert("File is too big! Max file size is 5MB.");
        return;
      }
      setFile(file);
    }
  };

  const toBase64 = (file: File) => {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = () => {
        resolve(reader.result);
      };
      reader.onerror = (error) => reject(error);
      reader.readAsDataURL(file as Blob);
    });
  };

  return (
    <main>
      <form onSubmit={handleSubmission}>
        <input
          type="file"
          accept="image/*"
          name="file"
          onChange={handleChange}
        />
        <input type="submit" value="Upload" />
        {file && (
          <div className="w-[300px] text-black p-4">
            <Image
              src={URL.createObjectURL(file)}
              alt="Uploaded image"
              width={300}
              height={300}
            />
          </div>

        )}
      </form>
    </main>
  );
}
