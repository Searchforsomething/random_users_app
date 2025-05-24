import { useParams } from 'react-router-dom';
import { useEffect, useState } from 'react';
import axios from 'axios';
import {
  Container, Typography, Card, CardContent, Avatar, Alert
} from '@mui/material';

function UserDetail() {
  const { id } = useParams();
  const [user, setUser] = useState(null);
  const [notFound, setNotFound] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    axios.get(`http://localhost:8000/${id}/`)
      .then(res => {
        setUser(res.data);
        setNotFound(false);
      })
      .catch(err => {
        if (err.response?.status === 404) {
          setNotFound(true);
        } else {
          console.error("Ошибка загрузки:", err);
        }
      })
      .finally(() => setLoading(false));
  }, [id]);

  if (loading) return <div className="p-4">Загрузка...</div>;

  if (notFound) {
    return (
      <Container sx={{ mt: 4 }}>
        <Alert severity="error">Пользователь не найден (404)</Alert>
      </Container>
    );
  }

  return (
    <Container sx={{ mt: 4 }}>
      <Card>
        <CardContent sx={{ display: 'flex', alignItems: 'center' }}>
          <Avatar src={user.thumbnail} sx={{ width: 100, height: 100, mr: 3 }} />
          <div>
            <Typography variant="h5">{user.first_name} {user.last_name}</Typography>
            <Typography>Email: {user.email}</Typography>
            <Typography>Телефон: {user.phone}</Typography>
            <Typography>Локация: {user.location}</Typography>
            <Typography>Пол: {user.gender}</Typography>
          </div>
        </CardContent>
      </Card>
    </Container>
  );
}

export default UserDetail;
