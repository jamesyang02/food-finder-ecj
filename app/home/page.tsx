'use client'

import ImageUpload from "@/app/components/image_upload"
import { useEffect, useState } from 'react';

export default function Page() {
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('https://food-finder-dr3kfl0iz-james-yangs-projects-b85f648d.vercel.app/api/')
      .then(res => res.json())
      .then(data => {
        setMessage(data.message);
        setLoading(false);
      })
  }, [])

  return (
    <div>
        <p> {!loading ? message : "Loading.."}</p>
        <ImageUpload />
    </div>
)
}