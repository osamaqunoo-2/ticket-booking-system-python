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
  allBookings {
    id
    userId
    event
    date
  }
}


mutation {
  loginUser(email: "test@example.com", password: "123456")
}

mutation {
  registerUser(email: "test@example.com", username: "osama", password: "123456")
}


mutation {
  createPayment(payment: {
    userId: 1,
    bookingId: 5,
    amount: 99.99,
    method: "credit_card",
    status: "success"
  })
}

mutation {
  allPayments {
    id
    userId
    bookingId
    amount
    method
    status
    timestamp
    
  }
}
