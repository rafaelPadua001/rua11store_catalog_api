// src/supabase.js
import { createClient } from '@supabase/supabase-js'

const supabaseUrl = 'https://hkoiwompbdeldmoznpxc.supabase.co'
const supabaseKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imhrb2l3b21wYmRlbGRtb3pucHhjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDI5MTI5NzIsImV4cCI6MjA1ODQ4ODk3Mn0.LwF_Rcm4zK8F1RC5kfuoR9eZdr5SvWcQuPSY0cpjq7U'

export const supabase = createClient(supabaseUrl, supabaseKey)
