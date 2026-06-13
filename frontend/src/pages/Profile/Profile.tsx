import { useState, useEffect } from 'react'
import { useParams } from 'react-router-dom'
import { usersAPI } from '../../services/api'
import { useAuthStore } from '../../store/authStore'

interface UserProfile {
  id: string
  username: string
  email: string
  phone: string
  age: number
  gender: string
  followers_count: number
  following_count: number
  posts_count: number
}

interface ProfileProps {
  isMyProfile?: boolean
}

const Profile = ({ isMyProfile = false }: ProfileProps) => {
  const { userId } = useParams()
  const { user: currentUser } = useAuthStore()
  const [profile, setProfile] = useState<UserProfile | null>(null)
  const [loading, setLoading] = useState(true)
  const [isFollowing, setIsFollowing] = useState(false)

  useEffect(() => {
    loadProfile()
  }, [userId])

  const loadProfile = async () => {
    try {
      if (isMyProfile) {
        const response = await usersAPI.getUser(currentUser?.id || '')
        setProfile(response.data)
      } else if (userId) {
        const response = await usersAPI.getUser(userId)
        setProfile(response.data)
      }
    } catch (error) {
      console.error('Failed to load profile:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleFollow = async () => {
    if (!profile) return
    try {
      await usersAPI.follow(profile.id)
      setIsFollowing(!isFollowing)
    } catch (error) {
      console.error('Failed to follow user:', error)
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-gray-500">Loading profile...</div>
      </div>
    )
  }

  if (!profile) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-gray-500">Profile not found</div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-2xl mx-auto px-4 py-8">
        {/* Profile Header */}
        <div className="bg-white rounded-lg shadow-md p-8 mb-6">
          <div className="flex items-center mb-6">
            <div className="w-20 h-20 bg-gradient-to-br from-primary to-secondary rounded-full flex items-center justify-center text-white text-3xl font-bold">
              {profile.username.charAt(0).toUpperCase()}
            </div>
            <div className="ml-6">
              <h1 className="text-3xl font-bold">{profile.username}</h1>
              <p className="text-gray-600">{profile.email}</p>
            </div>
          </div>

          <div className="grid grid-cols-3 gap-4 mb-6">
            <div className="text-center">
              <p className="text-2xl font-bold text-primary">{profile.posts_count}</p>
              <p className="text-gray-600">Posts</p>
            </div>
            <div className="text-center">
              <p className="text-2xl font-bold text-primary">{profile.followers_count}</p>
              <p className="text-gray-600">Followers</p>
            </div>
            <div className="text-center">
              <p className="text-2xl font-bold text-primary">{profile.following_count}</p>
              <p className="text-gray-600">Following</p>
            </div>
          </div>

          <div className="text-gray-700 space-y-2 mb-6">
            <p><strong>Phone:</strong> {profile.phone}</p>
            <p><strong>Age:</strong> {profile.age}</p>
            <p><strong>Gender:</strong> {profile.gender}</p>
          </div>

          {!isMyProfile && (
            <button
              onClick={handleFollow}
              className={`px-6 py-2 rounded-lg font-semibold transition ${
                isFollowing
                  ? 'bg-gray-300 text-gray-800 hover:bg-gray-400'
                  : 'bg-primary text-white hover:bg-blue-600'
              }`}
            >
              {isFollowing ? 'Unfollow' : 'Follow'}
            </button>
          )}
        </div>
      </div>
    </div>
  )
}

export default Profile
