#!/bin/bash

echo "Starting AI Comic Factory Frontend..."
echo

cd frontend

echo "Installing dependencies..."
npm install

echo
echo "Starting Next.js development server..."
echo "Frontend will be available at: http://localhost:3000"
echo
npm run dev 