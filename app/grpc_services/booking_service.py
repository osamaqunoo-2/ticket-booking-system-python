from app.grpc_services import booking_pb2, booking_pb2_grpc

# قاعدة بيانات وهمية
bookings = []
next_id = 1

class BookingService(booking_pb2_grpc.BookingServiceServicer):
    def CreateBooking(self, request, context):
        global next_id
        booking = booking_pb2.Booking(
            id=next_id,
            user_id=request.user_id,
            event=request.event,
            date=request.date
        )
        bookings.append(booking)
        next_id += 1
        return booking_pb2.BookingResponse(
            message="Booking created successfully!",
            success=True
        )

    def DeleteBooking(self, request, context):
        global bookings
        for b in bookings:
            if b.id == request.booking_id:
                bookings.remove(b)
                return booking_pb2.BookingResponse(
                    message="Booking deleted.",
                    success=True
                )
        return booking_pb2.BookingResponse(
            message="Booking not found.",
            success=False
        )

    def GetAllBookings(self, request, context):
        print("📥 GetAllBookings called")
        for b in bookings:
            print(f"📤 Sending booking: {b}")
            yield b  # ✅ لأن b هو كائن من نوع booking_pb2.Booking