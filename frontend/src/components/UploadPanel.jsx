import { useState } from "react"
import axios from "axios"

export default function UploadPanel() {

  // Track which file user selected
  const [file, setFile] = useState(null)

  // Track upload status message
  const [status, setStatus] = useState("")

  // Track if upload is in progress
  const [loading, setLoading] = useState(false)

  // Track if upload was successful
  const [uploaded, setUploaded] = useState(false)


  const handleUpload = async () => {
    // Don't do anything if no file selected
    if (!file) return

    // FormData is how you send files over HTTP
    // Like filling a form with a file attachment
    const formData = new FormData()
    formData.append("file", file)
    // "file" must match the parameter name in FastAPI:
    // async def upload_pdf(file: UploadFile = File(...))

    setLoading(true)   // show loading state
    setStatus("")      // clear previous status

    try {
      // Send file to our FastAPI backend
      // const res = await axios.post(
      //   "http://localhost:8000/upload",
      //   formData
      //   // Note: no Content-Type header needed
      //   // axios sets it automatically for FormData
      // )

      // Deploying to production → use VITE_API_URL from .env for backend URL
      const res = await axios.post(
        `${import.meta.env.VITE_API_URL}/upload`,
        formData
      )

      

      // Success!
      setStatus("✅ " + res.data.message)
      setUploaded(true)

    } catch (err) {
      // Something went wrong
      setStatus("Error!! Upload failed.")
      setUploaded(false)

    } finally {
      // Runs whether success or error
      setLoading(false)
    }
  }


  return (
    <div className="w-72 bg-gray-50 border-r border-gray-200 p-6
                    flex flex-col gap-4 h-screen">

      {/* Title */}
      <div>
        <h2 className="text-lg font-bold text-gray-800">Upload PDF</h2>
        <p className="text-xs text-gray-500 mt-1">
          Upload a document and ask questions about it in the chat! Supported file type: PDF.
        </p>
      </div>

      {/* Divider */}
      <hr className="border-gray-200" />

      {/* File picker */}
      <div className="flex flex-col gap-2">
        <label className="text-sm font-medium text-gray-700">
          Select PDF file
        </label>
        <input
          type="file"
          accept=".pdf"
          onChange={(e) => {
            setFile(e.target.files[0])  // save selected file
            setStatus("")               // clear old status
            setUploaded(false)          // reset uploaded state
          }}
          className="text-sm text-gray-500 file:mr-3 file:py-1 file:px-3
                     file:rounded-lg file:border-0 file:text-sm
                     file:bg-blue-50 file:text-blue-700
                     hover:file:bg-blue-100 cursor-pointer"
        />
      </div>

      {/* Show selected filename */}
      {file && (
        <p className="text-xs text-gray-500 truncate">
          Selected: {file.name}
        </p>
      )}

      {/* Upload button */}
      <button
        onClick={handleUpload}
        disabled={!file || loading}
        className="bg-blue-600 text-white py-2 px-4 rounded-xl
                   hover:bg-blue-700 disabled:opacity-50
                   disabled:cursor-not-allowed transition-colors
                   font-medium text-sm"
      >
        {loading ? "Uploading & Processing..." : "Upload & Ingest PDF"}
      </button>

      {/* Status message */}
      {status && (
        <div className={`text-sm p-3 rounded-lg ${
          uploaded
            ? "bg-green-50 text-green-700 border border-green-200"
            : "bg-red-50 text-red-700 border border-red-200"
        }`}>
          {status}
        </div>
      )}

      {/* Instructions */}
      <div className="mt-auto">
        <hr className="border-gray-200 mb-4" />
        <p className="text-xs text-gray-400 leading-relaxed">
            Created by Dhruv
        </p>
      </div>

    </div>
  )
}