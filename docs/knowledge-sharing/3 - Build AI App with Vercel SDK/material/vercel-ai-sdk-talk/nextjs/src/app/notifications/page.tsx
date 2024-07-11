'use client';

import { experimental_useObject as useObject } from 'ai/react';
import { notificationSchema } from '../api/notifications/schema';

export default function Page() {
  const { setInput, object } = useObject({
    api: '/api/notifications',
    schema: notificationSchema,
  });

  return (
    <div>
      <button
        onClick={async () => {
          setInput('Messages during finals week.');
        }}
      >
        Generate notifications
      </button>

      {object?.notifications?.map((notification, index) => (
        <div className='bg-slate-500 m-2 p-2' key={index}>
          <p>{notification?.name}</p>
          <p>{notification?.message}</p>
        </div>
      ))}
    </div>
  );
}