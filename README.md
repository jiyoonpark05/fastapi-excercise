# FastAPI Excercise

RESTful API with FastAPI to provide access to the mongo data

### Start

To start the FastAPI application, run the following command:

```bash
docker-compose up
```

During the process command run python script at `scripts/fetch_fake_data.py` this script fetch and store data from JSONPlaceholder - Free Fake REST API.

Once the process completes, you can navigate to `localhost:8000` to access the API.

```json
{
  "message": "API Development Exercise"
}
```

Backend documentation is available at `http://localhost:8000/docs`

![API Docs](assets/fast_api_docs.png)

### Features

**Posts**

Data structure of `posts_collection`

```json
{
  "_id": "665634e18d58f4905eb70edb",
  "userId": 1,
  "id": 1,
  "title": "example title",
  "body": "example body"
}
```

The API provides the following features for posts:

- Retrieve entire posts: Optionally filter posts by `userId`, `title`, or `body`(contents)
- Retrieve a specific post by id: Fetch a post using its unique identifier
- Create new post
- Update a post: Modify the title and body of an existing post
- Delete post
- Count the number of posts for a selected user

**2. Comments**

Data structure of `comments_collection`

```json
{
  "_id": "665634e28d58f4905eb70f3f",
  "postId": 1,
  "id": 1,
  "name": "name",
  "email": "Eliseo@gardner.biz",
  "body": "example body"
}
```

The API provides the following features for comments:

- Retrieve entire comments: Optionally filter comments by `postId`
- Retrieve a specific comment by `id`: Fetch a comment using its unique identifier
- Create new comment
- Update a comment: Modify the body(content) of an existing comment
- Delete comment
- Count the number of comments for a selected user by email
