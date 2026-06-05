import { useState } from "react"
import UploadPanel from "./components/UploadPanel"
import ChatWindow from "./components/ChatWindow"

export default function App() {
  const [darkMode, setDarkMode] = useState(false)

  return (
    <div className={`flex h-screen overflow-hidden ${
      darkMode ? "bg-gray-900" : "bg-white"
    }`}>
      <UploadPanel darkMode={darkMode} />
      <ChatWindow darkMode={darkMode} setDarkMode={setDarkMode} />
    </div>
  )
}