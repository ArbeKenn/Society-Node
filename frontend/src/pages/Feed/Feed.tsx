import { useState, useEffect } from 'react'
import { postsAPI } from '../../services/api'

interface Post {
  id: string
  author: {
    username: string
    id: string
  }
  content: string
  created_at: string
  likes_count: number
  comments_count: number
}

const Feed = () => {
  const [posts, setPosts] = useState<Post[]>([])
  const [loading, setLoading] = useState(true)
  const [newPostContent, setNewPostContent] = useState('')

  useEffect(() => {
    loadPosts()
  }, [])

  const loadPosts = async () => {
    try {
      const response = await postsAPI.getAllPosts()
      setPosts(response.data.posts || [])
    } catch (error) {
      console.error('Failed to load posts:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleCreatePost = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!newPostContent.trim()) return

    try {
      await postsAPI.createPost(newPostContent)
      setNewPostContent('')
      loadPosts()
    } catch (error) {
      console.error('Failed to create post:', error)
    }
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-2xl mx-auto px-4 py-8">
        {/* Create Post Form */}
        <div className="bg-white rounded-lg shadow-md p-6 mb-6">
          <form onSubmit={handleCreatePost}>
            <textarea
              value={newPostContent}
              onChange={(e) => setNewPostContent(e.target.value)}
              placeholder="What's on your mind?"
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary resize-none"
              rows={3}
            />
            <button
              type="submit"
              disabled={!newPostContent.trim()}
              className="mt-4 bg-primary hover:bg-blue-600 text-white font-semibold py-2 px-6 rounded-lg transition disabled:opacity-50"
            >
              Post
            </button>
          </form>
        </div>

        {/* Posts List */}
        <div className="space-y-4">
          {loading ? (
            <div className="text-center py-8 text-gray-500">Loading posts...</div>
          ) : posts.length === 0 ? (
            <div className="text-center py-8 text-gray-500">No posts yet</div>
          ) : (
            posts.map((post) => (
              <div key={post.id} className="bg-white rounded-lg shadow-md p-6">
                <div className="flex items-center mb-3">
                  <div className="w-10 h-10 bg-gradient-to-br from-primary to-secondary rounded-full flex items-center justify-center text-white font-bold">
                    {post.author.username.charAt(0).toUpperCase()}
                  </div>
                  <div className="ml-3">
                    <h3 className="font-semibold">{post.author.username}</h3>
                    <p className="text-sm text-gray-500">
                      {new Date(post.created_at).toLocaleDateString()}
                    </p>
                  </div>
                </div>
                <p className="text-gray-800 mb-4">{post.content}</p>
                <div className="flex space-x-6 text-gray-600 text-sm">
                  <button className="hover:text-primary transition">
                    👍 {post.likes_count}
                  </button>
                  <button className="hover:text-primary transition">
                    💬 {post.comments_count}
                  </button>
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  )
}

export default Feed
