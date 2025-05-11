mutation {
  createBooking(booking: {
    userId: 1,
    event: "Tech Conference",
    date: "2025-06-01"
  })
}

mutation {
  deleteBooking(bookingId: 1)
}

mutation {
  allBookings {
    id
    userId
    event
    date
  }
}

mutation {
  loginUser(email: "osama@gmail.com", password: "123456")
}

mutation {
  registerUser(email: "test@example.com", username: "osama", password: "123456")
}