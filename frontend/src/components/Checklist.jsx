import React, { useEffect, useState } from 'react'
import axios from 'axios'

const apiBase = '/api/'

export default function Checklist(){
  const [checklists, setChecklists] = useState([])

  useEffect(() => {
    fetchLists()
  }, [])

  const fetchLists = async () => {
    try{
      const res = await axios.get(apiBase + 'checklists/')
      setChecklists(res.data)
    }catch(e){
      console.error(e)
    }
  }

  const toggleItem = async (item) => {
    try{
      await axios.patch(apiBase + 'items/' + item.id + '/', { is_done: !item.is_done })
      setChecklists(prev => prev.map(cl => ({
        ...cl,
        items: cl.items.map(i => i.id === item.id ? { ...i, is_done: !i.is_done } : i)
      })))
    }catch(e){
      console.error(e)
    }
  }

  return (
    <div>
      {checklists.map(cl => (
        <div key={cl.id} className="mb-6 bg-white p-4 rounded-2xl shadow">
          <h2 className="text-xl font-semibold mb-3">{cl.name}</h2>
          <ul>
            {cl.items.map(item => (
              <li key={item.id} className={`flex justify-between items-center mb-2 p-2 border rounded-xl cursor-pointer ${item.is_done ? 'bg-green-50' : 'bg-gray-50'}`} onClick={() => toggleItem(item)}>
                <span>{item.title}</span>
                {item.is_done && <span>✅</span>}
              </li>
            ))}
          </ul>
        </div>
      ))}
    </div>
  )
}
