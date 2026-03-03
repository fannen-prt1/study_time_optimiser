import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';
import { sessionService } from '../../services/sessionService';
import type { StudySession, CreateSessionRequest, CompleteSessionRequest } from '../../types';

interface SessionsState {
  sessions: StudySession[];
  activeSession: StudySession | null;
  isLoading: boolean;
  error: string | null;
}

const initialState: SessionsState = {
  sessions: [],
  activeSession: null,
  isLoading: false,
  error: null,
};

// Async thunks
export const fetchSessions = createAsyncThunk(
  'sessions/fetchAll',
  async (
    params: { subject_id?: string; status?: string; skip?: number; limit?: number } | undefined,
    { rejectWithValue }
  ) => {
    try {
      return await sessionService.getAll(params);
    } catch (error) {
      return rejectWithValue(error instanceof Error ? error.message : 'Failed to fetch sessions');
    }
  }
);

export const createSession = createAsyncThunk(
  'sessions/create',
  async (data: CreateSessionRequest, { rejectWithValue }) => {
    try {
      return await sessionService.create(data);
    } catch (error) {
      return rejectWithValue(error instanceof Error ? error.message : 'Failed to create session');
    }
  }
);

export const startSession = createAsyncThunk(
  'sessions/start',
  async (id: string, { rejectWithValue }) => {
    try {
      return await sessionService.start(id);
    } catch (error) {
      return rejectWithValue(error instanceof Error ? error.message : 'Failed to start session');
    }
  }
);

export const pauseSession = createAsyncThunk(
  'sessions/pause',
  async (id: string, { rejectWithValue }) => {
    try {
      return await sessionService.pause(id);
    } catch (error) {
      return rejectWithValue(error instanceof Error ? error.message : 'Failed to pause session');
    }
  }
);

export const resumeSession = createAsyncThunk(
  'sessions/resume',
  async (id: string, { rejectWithValue }) => {
    try {
      return await sessionService.resume(id);
    } catch (error) {
      return rejectWithValue(error instanceof Error ? error.message : 'Failed to resume session');
    }
  }
);

export const completeSession = createAsyncThunk(
  'sessions/complete',
  async ({ id, data }: { id: string; data: CompleteSessionRequest }, { rejectWithValue }) => {
    try {
      return await sessionService.complete(id, data);
    } catch (error) {
      return rejectWithValue(
        error instanceof Error ? error.message : 'Failed to complete session'
      );
    }
  }
);

export const deleteSession = createAsyncThunk(
  'sessions/delete',
  async (id: string, { rejectWithValue }) => {
    try {
      await sessionService.delete(id);
      return id;
    } catch (error) {
      return rejectWithValue(error instanceof Error ? error.message : 'Failed to delete session');
    }
  }
);

// Slice
const sessionsSlice = createSlice({
  name: 'sessions',
  initialState,
  reducers: {
    clearError: (state) => {
      state.error = null;
    },
    setActiveSession: (state, action: PayloadAction<StudySession | null>) => {
      state.activeSession = action.payload;
    },
  },
  extraReducers: (builder) => {
    // Fetch all
    builder
      .addCase(fetchSessions.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(fetchSessions.fulfilled, (state, action) => {
        state.isLoading = false;
        state.sessions = action.payload;
        // Auto-detect active session
        const active = action.payload.find(
          (s) => s.status === 'active' || s.status === 'paused'
        );
        if (active) {
          state.activeSession = active;
        }
      })
      .addCase(fetchSessions.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload as string;
      });

    // Create
    builder
      .addCase(createSession.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(createSession.fulfilled, (state, action) => {
        state.isLoading = false;
        state.sessions.unshift(action.payload);
      })
      .addCase(createSession.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload as string;
      });

    // Start
    builder.addCase(startSession.fulfilled, (state, action) => {
      const index = state.sessions.findIndex((s) => s.id === action.payload.id);
      if (index !== -1) state.sessions[index] = action.payload;
      state.activeSession = action.payload;
    });

    // Pause
    builder.addCase(pauseSession.fulfilled, (state, action) => {
      const index = state.sessions.findIndex((s) => s.id === action.payload.id);
      if (index !== -1) state.sessions[index] = action.payload;
      state.activeSession = action.payload;
    });

    // Resume
    builder.addCase(resumeSession.fulfilled, (state, action) => {
      const index = state.sessions.findIndex((s) => s.id === action.payload.id);
      if (index !== -1) state.sessions[index] = action.payload;
      state.activeSession = action.payload;
    });

    // Complete
    builder.addCase(completeSession.fulfilled, (state, action) => {
      const index = state.sessions.findIndex((s) => s.id === action.payload.id);
      if (index !== -1) state.sessions[index] = action.payload;
      state.activeSession = null;
    });

    // Delete
    builder.addCase(deleteSession.fulfilled, (state, action) => {
      state.sessions = state.sessions.filter((s) => s.id !== action.payload);
      if (state.activeSession?.id === action.payload) {
        state.activeSession = null;
      }
    });
  },
});

export const { clearError } = sessionsSlice.actions;
export default sessionsSlice.reducer;
