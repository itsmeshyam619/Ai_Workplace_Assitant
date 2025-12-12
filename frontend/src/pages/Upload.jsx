import React, {useState} from 'react'
import axios from 'axios'

export default function Upload(){
  const [file, setFile] = useState(null)
  const [status, setStatus] = useState(null)

  const submit = async (e) =>{
    e.preventDefault()
    if(!file) return setStatus({error: 'No file selected'})
    const fd = new FormData()
    fd.append('file', file)
    setStatus({loading: true})
    try{
      const res = await axios.post('/api/upload', fd, {headers: {'Content-Type':'multipart/form-data'}})
      setStatus({success: res.data.message + ' ('+res.data.chunks_stored+' chunks)'})
    }catch(err){
      setStatus({error: err?.response?.data?.detail || err.message})
    }
  }

  return (
    <div>
      <h1 className="text-2xl font-semibold mb-4">Upload document</h1>
      <form onSubmit={submit} className="space-y-4">
        <input type="file" onChange={e=>setFile(e.target.files[0])} />
        <div>
          <button className="bg-blue-600 text-white px-4 py-2 rounded">Upload</button>
        </div>
      </form>
      <div className="mt-4">
        {status?.loading && <div>Processing...</div>}
        {status?.success && <div className="text-green-600">{status.success}</div>}
        {status?.error && <div className="text-red-600">{status.error}</div>}
      </div>
    </div>
  )
}
