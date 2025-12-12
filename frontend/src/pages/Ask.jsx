import React, {useState} from 'react'
import axios from 'axios'

export default function Ask(){
  const [question, setQuestion] = useState('')
  const [answer, setAnswer] = useState(null)
  const [error, setError] = useState(null)

  const submit = async (e) =>{
    e.preventDefault()
    setError(null)
    setAnswer(null)
    if(!question.trim()) return setError('Question cannot be empty')
    try{
      const res = await axios.post('/api/query', {question})
      setAnswer(res.data.answer)
    }catch(err){
      setError(err?.response?.data?.detail || err.message)
    }
  }

  return (
    <div>
      <h1 className="text-2xl font-semibold mb-4">Ask a question</h1>
      <form onSubmit={submit} className="space-y-4">
        <textarea rows={4} className="w-full p-2 border" value={question} onChange={e=>setQuestion(e.target.value)} />
        <div>
          <button className="bg-blue-600 text-white px-4 py-2 rounded">Ask</button>
        </div>
      </form>
      <div className="mt-4">
        {answer && <div className="p-4 bg-gray-50 border">{answer}</div>}
        {error && <div className="text-red-600">{error}</div>}
      </div>
    </div>
  )
}
