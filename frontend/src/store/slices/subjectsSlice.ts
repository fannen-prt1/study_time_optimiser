import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';
import { subjectService } from '../../services/subjectService';
import type { Subject, CreateSubjectRequest } from '../../types';

interface SubjectsState {
  subjects: Subject[];
  selectedSubject: Subject | null;
  isLoading: boolean;
  error: string | null;
}

const initialState: SubjectsState = {
  subjects: [],
  selectedSubject: null,
  isLoading: false,
  error: null,
};

// Async thunks
export const fetchSubjects = createAsyncThunk(
  'subjects/fetchAll',
  async (includeArchived: boolean = false, { rejectWithValue }) => {
    try {
      return await subjectService.getAll(includeArchived);
    } catch (error) {
      return rejectWithValue(error instanceof Error ? error.message : 'Failed to fetch subjects');
    }
  }
);

export const createSubject = createAsyncThunk(
  'subjects/create',
  async (data: CreateSubjectRequest, { rejectWithValue }) => {
    try {
      return await subjectService.create(data);
    } catch (error) {
      return rejectWithValue(error instanceof Error ? error.message : 'Failed to create subject');
    }
  }
);

export const updateSubject = createAsyncThunk(
  'subjects/update',
  async ({ id, data }: { id: string; data: Partial<CreateSubjectRequest> }, { rejectWithValue }) => {
    try {
      return await subjectService.update(id, data);
    } catch (error) {
      return rejectWithValue(error instanceof Error ? error.message : 'Failed to update subject');
    }
  }
);

export const deleteSubject = createAsyncThunk(
  'subjects/delete',
  async (id: string, { rejectWithValue }) => {
    try {
      await subjectService.delete(id);
      return id;
    } catch (error) {
      return rejectWithValue(error instanceof Error ? error.message : 'Failed to delete subject');
    }
  }
);

export const archiveSubject = createAsyncThunk(
  'subjects/archive',
  async (id: string, { rejectWithValue }) => {
    try {
      return await subjectService.archive(id);
    } catch (error) {
      return rejectWithValue(error instanceof Error ? error.message : 'Failed to archive subject');
    }
  }
);

export const unarchiveSubject = createAsyncThunk(
  'subjects/unarchive',
  async (id: string, { rejectWithValue }) => {
    try {
      return await subjectService.unarchive(id);
    } catch (error) {
      return rejectWithValue(
        error instanceof Error ? error.message : 'Failed to unarchive subject'
      );
    }
  }
);

// Slice
const subjectsSlice = createSlice({
  name: 'subjects',
  initialState,
  reducers: {
    clearError: (state) => {
      state.error = null;
    },
    setSelectedSubject: (state, action: PayloadAction<Subject | null>) => {
      state.selectedSubject = action.payload;
    },
  },
  extraReducers: (builder) => {
    // Fetch all
    builder
      .addCase(fetchSubjects.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(fetchSubjects.fulfilled, (state, action) => {
        state.isLoading = false;
        state.subjects = action.payload;
      })
      .addCase(fetchSubjects.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload as string;
      });

    // Create
    builder
      .addCase(createSubject.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(createSubject.fulfilled, (state, action) => {
        state.isLoading = false;
        state.subjects.push(action.payload);
      })
      .addCase(createSubject.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload as string;
      });

    // Update
    builder
      .addCase(updateSubject.fulfilled, (state, action) => {
        const index = state.subjects.findIndex((s) => s.id === action.payload.id);
        if (index !== -1) {
          state.subjects[index] = action.payload;
        }
      })
      .addCase(updateSubject.rejected, (state, action) => {
        state.error = action.payload as string;
      });

    // Delete
    builder
      .addCase(deleteSubject.fulfilled, (state, action) => {
        state.subjects = state.subjects.filter((s) => s.id !== action.payload);
      })
      .addCase(deleteSubject.rejected, (state, action) => {
        state.error = action.payload as string;
      });

    // Archive
    builder.addCase(archiveSubject.fulfilled, (state, action) => {
      const index = state.subjects.findIndex((s) => s.id === action.payload.id);
      if (index !== -1) {
        state.subjects[index] = action.payload;
      }
    });

    // Unarchive
    builder.addCase(unarchiveSubject.fulfilled, (state, action) => {
      const index = state.subjects.findIndex((s) => s.id === action.payload.id);
      if (index !== -1) {
        state.subjects[index] = action.payload;
      }
    });
  },
});

export const { clearError } = subjectsSlice.actions;
export default subjectsSlice.reducer;
